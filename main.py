import os
from logging import getLogger, StreamHandler, INFO
import asyncio
import time
import random

import requests
import streamlit as st
from dotenv import load_dotenv

from package.marcov import SingleMarcov

load_dotenv()

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(int(os.environ.get("LOG_LEVEL", INFO)))
logger.setLevel(int(os.environ.get("LOG_LEVEL", INFO)))
logger.addHandler(handler)
logger.propagate = False


st.set_page_config(
    page_title="1文字マルコフ連鎖",
    page_icon="⛓️‍💥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "https://discord.com/invite/webmania/",
        "Get help": "https://github.com/takechi-scratch/marcov_1char/"
    }
)

st.title("1文字マルコフ連鎖")


def fetch_data():
    """GASの取得は時間がかかるので、初期化時の1回だけ"""
    res = requests.get(os.environ["DATA_URL"])

    return res.text


def generate_txt(max_length: int = 100, auto_convert: bool = False):
    text = st.session_state.model.generate_text(max_length=max_length)
    if auto_convert:
        pass
    else:
        for x in text:
            yield x
            if random.random() < 0.3:
                time.sleep(0.1)


async def main():
    # 初期設定
    if "data" not in st.session_state:
        with st.spinner("データを取得中です、しばらくお待ちください..."):
            res = requests.get(os.environ["DATA_URL"])
            st.session_state.data = res.content.decode("utf-8")
            logger.debug(st.session_state.data)

        with st.expander("モデルの準備中です、しばらくお待ちください..."):
            st.session_state.model = SingleMarcov(text=st.session_state.data)

    auto_convert = st.toggle("自動で変換する(準備中)", False)
    start_generate = st.button("生成開始", type="primary")

    generate_area = st.container(border=True)

    if start_generate:
        with generate_area:
            status = st.empty()

            with st.spinner("生成中..."):
                if auto_convert:
                    text = st.markdown("")
                    for generating_text in generate_txt(auto_convert=True):
                        text.text = generating_text
                else:
                    st.write_stream(generate_txt)

            status.caption("生成完了")
    else:
        generate_area.caption("ここにテキストが生成されます")


asyncio.run(main())
