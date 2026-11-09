package com.zevorix.assistant

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch

class MainViewModel(application: Application) : AndroidViewModel(application) {
    private val localAiService = LocalAiService(application)

    private val _uiState = MutableStateFlow("")
    val uiState: StateFlow<String> = _uiState.asStateFlow()

    fun askLocalAi(prompt: String) {
        viewModelScope.launch {
            try {
                _uiState.value = "جاري التفكير محلياً..."
                val fullResponse = StringBuilder()
                localAiService.generateStream(prompt).collectLatest { chunk ->
                    fullResponse.append(chunk)
                    _uiState.value = fullResponse.toString()
                }
            } catch (e: Exception) {
                _uiState.value = "حدث خطأ: ${e.localizedMessage}"
            }
        }
    }
}
