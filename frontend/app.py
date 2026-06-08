import streamlit as st
import requests

# إعدادات الصفحة
st.set_page_config(
    page_title="YouTube Summarizer",
    page_icon="🎬",
    layout="wide"
)

# الـ Sidebar - About
with st.sidebar:
    st.header("📖 About")
    st.info("""
    **YouTube Summarizer** هو تطبيق ذكي يلخص فيديوهات YouTube تلقائياً!
    
    ### المميزات:
    - استخراج نص الفيديو (Transcript)
    - تلخيص ذكي بـ AI
    - واجهة سهلة وسريعة
    
    ### كيفية الاستخدام:
    1. ادخل رابط YouTube
    2. اضغط "Summarize" أو Enter
    3. اقرأ الملخص
    
    **بني بـ:** Flask + Streamlit + Google Gemini
    """)

# العنوان الرئيسي
st.title("🎬 YouTube Summarizer")
st.markdown("""
تلخيص فيديوهات YouTube بذكاء اصطناعي حقيقي! 
استخرج أهم النقاط من أي فيديو في ثوانٍ.
""")

st.divider()

# قسم الإدخال
st.subheader("📝 أدخل رابط YouTube")

with st.form(key='summarize_form'):
    url = st.text_input(
        "YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed"
    )
    
    submit_button = st.form_submit_button(
        "🚀 Summarize",
        use_container_width=True
    )


# معالجة الطلب
if submit_button:
    if not url:
        st.error("❌ الرجاء إدخال رابط YouTube")
    else:
        try:
            with st.spinner("⏳ جاري معالجة الفيديو..."):
                response = requests.post(
                    'https://youtube-summarizer-api-so0i.onrender.com/summarize',
                    json={'url': url},
                    timeout=30
                )
            
            if response.status_code == 200:
                result = response.json()
                
                # تحقق من وجود error في النتيجة
                if 'error' in result:
                    st.error(f"❌ خطأ: {result['error']}")
                else:
                    # رسالة النجاح (بعد التأكد من النتائج)
                    st.success("✅ تم التلخيص بنجاح!")
                    
                    # عرض النتائج
                    st.subheader("📊 النتائج")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        video_id = result.get('video_id', 'N/A')
                        if video_id and video_id != 'N/A':
                            st.metric("Video ID", video_id[:10] + "...")
                        else:
                            st.metric("Video ID", "N/A")
                    
                    with col2:
                        transcript = result.get('transcript', '')
                        transcript_length = len(transcript.split())
                        st.metric("عدد الكلمات", transcript_length)
                    
                    with col3:
                        summary = result.get('summary', '')
                        summary_length = len(summary.split())
                        st.metric("ملخص الكلمات", summary_length)
                    
                    st.divider()
                    
                    # عرض النص والملخص
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📄 النص الكامل")
                        st.text_area(
                            "Transcript",
                            result.get('transcript', 'No transcript'),
                            height=300,
                            disabled=True,
                            label_visibility="collapsed"
                        )
                    
                    with col2:
                        st.subheader("✨ الملخص الذكي")
                        st.info(result.get('summary', 'No summary'))
                    
                    st.balloons()
            
            else:
                st.error(f"❌ خطأ من السيرفر: {response.status_code}")
        
        except requests.exceptions.ConnectionError:
            st.error("❌ لا يمكن الاتصال بـ Flask Server. تأكد من أنه يعمل على https://youtube-summarizer-api-so0i.onrender.com/summarize")
        except requests.exceptions.Timeout:
            st.error("❌ انتهت مهلة الانتظار. حاول مرة أخرى.")
        except Exception as e:
            st.error(f"❌ حدث خطأ: {str(e)}")