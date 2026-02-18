import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Análise de Consumo de Energia", layout="centered")

st.title("🔌 Análise de Consumo de Energia Elétrica")

st.markdown("Informe os dados de consumo mensal para gerar análise estatística e previsão.")

# ==============================
# QUANTIDADE DE MESES
# ==============================

qtd_meses = st.number_input(
    "Quantos meses deseja informar? (mínimo 3 e máximo 12)",
    min_value=1,
    max_value=12,
    step=1
)

if qtd_meses < 3:
    st.warning("Dados insuficientes. É necessário informar no mínimo 3 meses.")
    st.stop()

# ==============================
# COLETA DOS DADOS
# ==============================

dados = []

for i in range(int(qtd_meses)):
    st.markdown(f"### Mês {i+1}")

    mes = st.text_input("Mês", key=f"mes_{i}")
    ano = st.number_input("Ano", min_value=2000, max_value=2100, step=1, key=f"ano_{i}")
    consumo = st.number_input("Consumo (kWh)", min_value=0.0, step=0.1, key=f"consumo_{i}")

    if mes:
        dados.append({
            "Mes/Ano": f"{mes}/{ano}",
            "Consumo (kWh)": consumo
        })

# ==============================
# PROCESSAMENTO
# ==============================

if len(dados) >= 3:

    df = pd.DataFrame(dados)

    st.subheader("💰 Valor da Energia")

    valor_kwh = st.number_input(
        "Qual é o valor do kWh (R$/kWh)?",
        min_value=0.0,
        step=0.01
    )

    confirmar = st.checkbox(f"Confirmo o valor de R$ {valor_kwh:.2f} por kWh")

    if confirmar:

        # Estatísticas
        media = df["Consumo (kWh)"].mean()
        mediana = df["Consumo (kWh)"].median()
        maximo = df["Consumo (kWh)"].max()
        minimo = df["Consumo (kWh)"].min()
        desvio_padrao = df["Consumo (kWh)"].std()
        amplitude = maximo - minimo

        consumo_diario = media / 30

        previsao = df["Consumo (kWh)"].tail(3).mean()
        valor_estimado = previsao * valor_kwh

        # ==============================
        # RELATÓRIO
        # ==============================

        st.subheader("📊 Estatística Descritiva")

        st.write({
            "Média (kWh)": round(media, 2),
            "Mediana (kWh)": round(mediana, 2),
            "Máximo (kWh)": round(maximo, 2),
            "Mínimo (kWh)": round(minimo, 2),
            "Desvio padrão (kWh)": round(desvio_padrao, 2),
            "Amplitude (kWh)": round(amplitude, 2)
        })

        st.subheader("📅 Consumo Médio Diário")
        st.write(f"{consumo_diario:.2f} kWh/dia")

        st.subheader("🔮 Previsão do Próximo Mês")
        st.write(f"{previsao:.2f} kWh")

        st.subheader("💡 Valor Estimado da Próxima Conta")
        st.write(f"R$ {valor_estimado:.2f}")

        # ==============================
        # GRÁFICO
        # ==============================

        st.subheader("📈 Consumo Mensal")

        plt.figure(figsize=(10, 5))
        sns.barplot(x="Mes/Ano", y="Consumo (kWh)", data=df)
        plt.axhline(media, linestyle='--', label=f"Média = {media:.1f} kWh")
        plt.xlabel("Mês/Ano")
        plt.ylabel("Consumo (kWh)")
        plt.title("Histórico de Consumo de Energia Elétrica")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        st.pyplot(plt)

        # ==============================
        # OBSERVAÇÃO FINAL
        # ==============================

        st.subheader("📝 Observação Técnica")

        st.write(
            "A previsão foi realizada utilizando média móvel simples "
            "com janela fixa de 3 meses, considerando os três últimos períodos informados."
        )
