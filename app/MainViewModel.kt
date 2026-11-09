// داخل MainViewModel.kt

// أضف هذه المتغيرات لدعم الـ Router والوضع الحالي
private val aiRouter: AiRouter = /* يتم حقن أو إنشاء الـ Router هنا مع تمرير الـ Context والـ Cloud client و LocalAiService */
var currentAiMode: AiMode by mutableStateOf(AiMode.AUTO)
    private set

fun setAiMode(mode: AiMode) {
    currentAiMode = mode
}

// دالة إرسال الرسالة للذكاء الاصطناعي (تلقائي أو محلي)
fun sendToAi(prompt: String) {
    viewModelScope.launch {
        // تحديث واجهة المستخدم أو إضافة رسالة المستخدم للقائمة
        repository.addUserMessage(prompt)
        
        // استخدام الـ Router لجلب الرد تدريجياً (Streaming)
        aiRouter.reply(prompt, currentAiMode)
            .catch { e -> 
                // التعامل مع الأخطاء وإظهارها للمستخدم
                repository.addAssistantMessage("حدث خطأ: ${e.localizedMessage}")
            }
            .collect { chunk ->
                // هنا يتم تحديث آخر رسالة للمساعد بالقطع (Chunks) القادمة تباعاً
                // سواء كانت متولدة من معالج الهاتف محلياً أو من السحاب
                updateOrAddAssistantChunk(chunk)
            }
    }
}
