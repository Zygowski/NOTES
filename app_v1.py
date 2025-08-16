
import streamlit as st
from openai import OpenAI

st.title("Generator krótkich opowiadań 📖")
st.write("""
Użyj tej aplikacji, aby wygenerować krótkie opowiadania. Wprowadź swój tekst w poniższym polu tekstowym,
a następnie kliknij przycisk 'Generuj'. ✨
""")

openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def create_story(story_prompt):
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """
                    Jesteś opowiadaczem historii.
                    Twórz krótkie opowiadania na podstawie podanego tekstu.
                    Opowiadania powinny być wciągające i zaskakujące.
                    Mają być zbudowane wokół struktury:
                    - wstęp
                    - rozwinięcie
                    - zakończenie

                    Opowiadanie nie powinno być krótsze niż 100 słów.
                """
            },
            {"role": "user", "content": story_prompt}
        ]
    )
    usage = {}
    if response.usage:
        usage = {
            "completion_tokens": response.usage.completion_tokens,
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        }

    return {
        "role": "assistant",
        "content": response.choices[0].message.content,
        "usage": usage,
    }

st.session_state['user_input'] = st.text_area("Wprowadź swój tekst:", max_chars=1000)
if st.button("Generuj 🚀", disabled=not st.session_state['user_input'].strip(), use_container_width=True):
    st.session_state['story'] = create_story(st.session_state['user_input'])

if st.session_state.get('story'):
    st.write("### Twoje wygenerowane opowiadanie:")
    st.write(st.session_state['story']['content'])

    st.download_button(
        label="Pobierz wygenerowane opowiadanie",
        data=st.session_state['story']['content'],
        file_name="wygenerowane_opowiadanie.txt",
        mime="text/plain",
        use_container_width=True,
    )
