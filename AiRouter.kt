package com.zevorix.assistant

import android.content.Context
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class AiRouter(context: Context) {
    private val localAiService = LocalAiService(context)

    fun routeQuery(prompt: String): Flow<String> = flow {
        try {
            // استدعاء الخدمة المحلية وتمرير النص مع تحديد نوع البيانات بوضوح لتجنب خطأ الـ Compiler
            localAiService.generateStream(prompt).collect { chunk: String ->
                emit(chunk)
            }
        } catch (e: Exception) {
            emit("حدث خطأ في الموجه المحلي: ${e.localizedMessage}")
        }
    }
}
