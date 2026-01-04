"""
Scroll utility for Streamlit
페이지 로드 시 스크롤을 맨 위로 이동
"""

import streamlit as st


def scroll_to_top():
    """페이지 스크롤을 맨 위로 이동"""
    st.markdown("""
        <script>
            // 메인 윈도우 스크롤 리셋
            window.scrollTo({top: 0, left: 0, behavior: 'instant'});
            
            // Streamlit 메인 컨테이너 스크롤 리셋
            const mainContainer = window.parent.document.querySelector('section.main');
            if (mainContainer) {
                mainContainer.scrollTo({top: 0, left: 0, behavior: 'instant'});
            }
            
            // App View Container 스크롤 리셋
            const stApp = window.parent.document.querySelector('[data-testid="stAppViewContainer"]');
            if (stApp) {
                stApp.scrollTo({top: 0, left: 0, behavior: 'instant'});
            }
            
            // Block Container 스크롤 리셋
            const blockContainer = window.parent.document.querySelector('.block-container');
            if (blockContainer) {
                blockContainer.scrollTo({top: 0, left: 0, behavior: 'instant'});
            }
        </script>
    """, unsafe_allow_html=True)


def scroll_to_element(element_id: str):
    """특정 요소로 스크롤 이동"""
    st.markdown(f"""
        <script>
            const element = document.getElementById('{element_id}');
            if (element) {{
                element.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}
        </script>
    """, unsafe_allow_html=True)
