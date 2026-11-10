package com.zevorix.assistant

import android.content.Context
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class AiRouter(context: Context) {
    private val localAiService = LocalAiService(context)
    private val appContext = context.applicationContext

    // دالة للتحقق من توفر الإنترنت
    private fun isNetworkAvailable(): Boolean {
        val connectivityManager = appContext.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        val network = connectivityManager.activeNetwork ?: return false
        val capabilities = connectivityManager.getNetworkCapabilities(network) ?: return false
        return capabilities.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET) &&
               capabilities.hasCapability(NetworkCapabilities.NET_CAPABILITY_VALIDATED)
    }

    fun routeQuery(prompt: String): Flow<String> = flow {
        // إذا لم يكن هناك إنترنت، استخدم النموذج المحلي مباشرة
        if (!isNetworkAvailable()) {
            localAiService.generateStream(prompt).collect { chunk: String ->
                emit(chunk)
            }
            return@flow
        }

        // إذا كان هناك إنترنت، يمكنك هنا استدعاء الخدمة السحابية (AiChatService)
        // أو الاستمرار في استخدام المحلي حسب رغبتك.
        // مثال: استخدام المحلي فقط:
        localAiService.generateStream(prompt).collect { chunk: String ->
            emit(chunk)
        }
    }
}