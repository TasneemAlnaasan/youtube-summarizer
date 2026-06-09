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
        st.error(" ⚠️ الرجاء إدخال رابط YouTube")
    else:
        try:
            with st.spinner(" ⏳ جاري معالجة الفيديو واستدعاء الذكاء الاصطناعي..."):
                response = requests.post(
                    'https://youtube-summarizer-api-isl5.onrender.com/summarize',
                    json={'url': url},
                    timeout=35
                )
            
            if response.status_code == 200:
                result = response.json()
                
                # 1️⃣ فحص أول: هل الباك اند أرسل خطأ صريح في مفتاح 'error'؟
                if 'error' in result:
                    st.error(f" ❌ خطأ: {result['error']}")
                
                # 2️⃣ الفحص الذكي الجديد: هل النص المستخرج عبارة عن رسالة خطأ وحظر؟
                elif "Error extracting transcript" in result.get('transcript', ''):
                    st.error(" 🚫 عذراً، فشلت العملية! يوتيوب قام بحظر السيرفر مؤقتاً (Too Many Requests).")
                    
                    # عرض تفاصيل المشكلة بشكل أنيق للمطور دون إيهام المستخدم بالنجاح
                    with st.expander("🔍 إظهار تفاصيل الخطأ الفني"):
                        st.warning(result.get('transcript'))
                        st.info(result.get('summary'))
                
                # 3️⃣ حالة النجاح الحقيقي الكامل 100%
                else:
                    st.success(" 🎉 تم التلخيص بنجاح !")
                    st.balloons()
                    
                    # عرض النتائج والإحصائيات
                    st.subheader(" 📊 النتائج الحية")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        video_id = result.get('video_id', 'N/A')
                        st.metric("Video ID", video_id if video_id else "N/A")
                    
                    with col2:
                        transcript = result.get('transcript', '')
                        transcript_length = len(transcript.split())
                        st.metric("عدد كلمات الفيديو", transcript_length)
                    
                    with col3:
                        summary = result.get('summary', '')
                        summary_length = len(summary.split())
                        st.metric("عدد كلمات الملخص", summary_length)
                    
                    st.divider()
                    
                    # عرض النصوص المقروءة في صناديق منظمة
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader(" 📄 النص الكامل المستخرج")
                        st.text_area("Transcript", transcript, height=250, disabled=True, label_visibility="collapsed")
                    
                    with col2:
                        st.subheader(" ✨ الملخص الذكي (Gemini)")
                        st.info(summary)
            
            else:
                st.error(f" ❌ خطأ من السيرفر السحابي: كود الاستجابة {response.status_code}")
        
        except requests.exceptions.ConnectionError:
            st.error(" 🔌 تعذر الاتصال بالباك اند. تأكد من أن سيرفر Render يعمل وحالته Live.")
        except requests.exceptions.Timeout:
            st.error(" ⏳ انتهت مهلة الانتظار (Timeout). السيرفر يستغرق وقتاً طويلًا للاستجابة.")
        except Exception as e:
            st.error(f" 🚨 حدث خطأ غير متوقع: {str(e)}")