package com.zevorix.ai.local

import android.content.Context
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

/** واجهة بسيطة: اربطها بخدمتك السحابية الحالية. */
interface CloudAiClient {
    suspend fun generate(prompt: String): String
}

enum class AiMode {
    AUTO,        // سحابي إن توفر الإنترنت، وإلا محلي
    LOCAL_ONLY,  // وضع الخصوصية المحلية
    CLOUD_ONLY
}

class AiRouter(
    private val appContext: Context,
    private val cloud: CloudAiClient,
    private val local: LocalAiService,
) {
    fun isOnline(): Boolean {
        val cm = appContext.getSystemService(ConnectivityManager::class.java) ?: return false
        val caps = cm.getNetworkCapabilities(cm.activeNetwork) ?: return false
        return caps.hasCapability(NetworkCapabilities.NET_CAPABILITY_VALIDATED)
    }

    /** يرجع الرد على شكل Flow موحّد (دفعة واحدة للسحابي، وعدة دفعات للمحلي). */
    fun reply(prompt: String, mode: AiMode): Flow<String> = flow {
        val useLocal = when (mode) {
            AiMode.LOCAL_ONLY -> true
            AiMode.CLOUD_ONLY -> false
            AiMode.AUTO -> !isOnline()
        }

        if (useLocal) {
            local.generateStream(prompt).collect { chunk ->
                emit(chunk)
            }
        } else {
            try {
                emit(cloud.generate(prompt))
            } catch (e: Exception) {
                // فشل السحابي في وضع AUTO → تراجع تلقائي إلى المحلي
                if (mode == AiMode.AUTO) {
                    local.generateStream(prompt).collect { chunk ->
                        emit(chunk)
                    }
                } else {
                    throw e
                }
            }
        }
    }
}

/* ------------------------------------------------------------------
 * مثال دمج في MainViewModel (عدّله ليناسب هيكلتك الحالية)
 * ------------------------------------------------------------------ */

data class ChatUiState(
    val reply: String = "",
    val isGenerating: Boolean = false,
    val mode: AiMode = AiMode.AUTO,
    val error: String? = null,
)

class MainViewModel(
    private val router: AiRouter,
    private val local: LocalAiService,
) : ViewModel() {

    private val _ui = MutableStateFlow(ChatUiState())
    val ui: StateFlow<ChatUiState> = _ui.asStateFlow()

    private var job: Job? = null

    fun setMode(mode: AiMode) = _ui.update { it.copy(mode = mode) }

    fun send(prompt: String) {
        job?.cancel()
        _ui.update { it.copy(reply = "", isGenerating = true, error = null) }

        job = viewModelScope.launch {
            router.reply(prompt, _ui.value.mode)
                .catch { e -> _ui.update { it.copy(error = e.message ?: "حدث خطأ") } }
                .collect { chunk -> _ui.update { it.copy(reply = it.reply + chunk) } }
            _ui.update { it.copy(isGenerating = false) }
        }
    }

    fun stop() {
        job?.cancel() // يوقف التوليد المحلي تلقائياً
        _ui.update { it.copy(isGenerating = false) }
    }

    override fun onCleared() {
        local.release()
        super.onCleared()
    }
}
