from openai import OpenAI
import streamlit as st
import requests
import os

class OpenAIEngine():

    def __init__(self,mode="",model="",prompt=""):
        self.client = OpenAI()
        if "memory" not in st.session_state:
            st.session_state["memory"] = [{}]
        if "image_number" not in st.session_state:
            st.session_state['image_number'] = 1
        if "image_folder" not in st.session_state:
            st.session_state["image_folder"] = os.path.join("..","images")
        self.change(mode,model,prompt)

    def change(self,mode,model,prompt):
        self.mode = mode
        self.model = model
        st.session_state["memory"][0] = {"role":"system","content":prompt}

    def generate_answer(self,prompt):
        st.session_state["memory"].append({"role":"user","content":prompt})
        memory = []
        for mem in st.session_state['memory']:
            if mem['role'] != "image assistant":
                memory.append(mem)
            else:
                memory = memory[:-1]
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=memory,
            stream=True,
            temperature=0,
        )
        response = st.write_stream(stream)
        response = {"role": "assistant", "content": response}
        st.session_state["memory"].append(response)
        print(st.session_state["memory"])
        print()

    def generate_image(self,prompt):
        image_data = self.client.images.generate(
                model=self.model,
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
        )
        image = requests.get(image_data.data[0].url,stream=True)
        if image.status_code == 200:
            image_path = os.path.join(st.session_state["image_folder"],
                                      f"{st.session_state['image_number']}.png")
            st.session_state["image_number"] += 1
            with open(image_path, 'wb') as f:
                for chunk in image:
                    f.write(chunk)
            st.session_state["memory"].append({"role":"user","content":prompt})
            st.session_state["memory"].append({"role": "image assistant", "content": image_path})
            st.image(image_path)