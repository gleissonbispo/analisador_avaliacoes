# =============================
# 🤖 Analisador de Avaliações com LLM Local
# =============================

# 📦 Bibliotecas
import streamlit as st
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from time import sleep

# =============================
# 📊 Classe de Saída Estruturada com Pydantic
# =============================
class AvaliacaoOutput(BaseModel):
    sentimento: str = Field(description="Sentimento geral da avaliação: 'Muito Positivo', 'Positivo', 'Neutro', 'Negativo', 'Muito Negativo'")
    ponto_principal: str = Field(description="Resumo do ponto mais relevante citado")
    palavra_chave: str = Field(description="Palavra-chave extraída da avaliação")
    resumo: str = Field(description="Resumo da avaliação em uma única frase")
    nota_satisfacao: int = Field(description="Nota estimada de satisfação do colaborador (0 a 10)")

# =============================
# ⚙️ Inicialização do Modelo LLM (Ollama local)
# =============================
llm = ChatOllama(model="gemma3:12b")  # Substitua pelo modelo desejado instalado localmente via Ollama
llm_estruturada = llm.with_structured_output(AvaliacaoOutput)

# =============================
# 🎨 Configuração da Interface
# =============================
st.set_page_config(page_title="Analisador de Avaliações", page_icon="📊", layout="centered")

with st.container():
    st.title("🤖 Analisador Inteligente de Avaliações")
    st.caption("Análise automática de sentimentos e principais insights de feedbacks com LLM local.")

    st.markdown("---")

# =============================
# ✏️ Entrada do Usuário
# =============================
st.subheader("📝 Insira ou cole a avaliação de um colaborador:")
avaliacao_usuario = st.text_area(
    label="Texto da avaliação",
    placeholder="Exemplo: 'A empresa oferece bons benefícios, mas a liderança é desorganizada.'",
    height=200
)

# =============================
# 🚀 Botão de Execução
# =============================
if st.button("🔍 Analisar Avaliação", use_container_width=True):
    if avaliacao_usuario.strip() == "":
        st.warning("⚠️ Por favor, cole ou escreva uma avaliação antes de continuar.")
    else:
        with st.status("💭 Pensando...", expanded=True) as status:
            resposta_modelo = llm_estruturada.invoke(avaliacao_usuario)
            sleep(1.5)
            status.update(label="✅ Análise Concluída", state="complete")

        # =============================
        # 📊 Resultados
        # =============================
        st.markdown("---")
        st.subheader("📈 Resultado da Análise")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🎯 Sentimento Geral**")
            st.success(resposta_modelo.sentimento)

            st.markdown("**🔑 Palavra-chave**")
            st.info(resposta_modelo.palavra_chave)

            st.markdown("**📉 Satisfação Estimada (0-10)**")
            st.code(f"{resposta_modelo.nota_satisfacao} / 10", language="markdown")

        with col2:
            st.markdown("**📌 Ponto Principal**")
            st.write(resposta_modelo.ponto_principal)

            st.markdown("**🧾 Resumo da Avaliação**")
            st.write(resposta_modelo.resumo)

        st.markdown("---")
        st.caption("🔐 Seus dados não são enviados para a nuvem. Tudo é processado localmente.")
