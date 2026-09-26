import json
import logging
from pathlib import Path

import joblib
import pandas as pd

from src.logging_config import configurar_logging


# Define o caminho absoluto do modelo a partir da localização deste arquivo.
# Dessa forma, o carregamento não depende do diretório em que o programa
# estiver sendo executado.
MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "churn_model.joblib"
)

# Threshold definido durante a etapa de avaliação dos modelos.
# Probabilidades iguais ou superiores a 0,40 serão classificadas como churn.
THRESHOLD = 0.40


configurar_logging()
logger = logging.getLogger(__name__)

# Carrega o pipeline treinado e persistido durante a etapa de modelagem.
# O arquivo contém tanto o pré-processamento dos dados quanto o modelo
# de Regressão Logística utilizado para estimar a probabilidade de churn.
modelo = joblib.load(MODEL_PATH)
logger.info("Modelo carregado com sucesso: %s; threshold=%.2f", MODEL_PATH, THRESHOLD)


def prever_churn(dados_cliente: dict) -> dict:
    """
    Calcula a probabilidade de churn de um cliente e retorna
    a classificação utilizando o threshold definido para o modelo.
    """

    # Converte os dados recebidos para DataFrame, formato esperado
    # pelo pipeline utilizado durante o treinamento.
    dados = pd.DataFrame([dados_cliente])
    logger.info("Executando predição para um cliente")

    # Obtém a probabilidade associada à classe positiva (churn = 1).
    probabilidade = modelo.predict_proba(dados)[0, 1]

    # Aplica o threshold selecionado durante a avaliação do modelo.
    previsao = int(probabilidade >= THRESHOLD)

    logger.info("Predição concluída; churn=%s", previsao)

    return {
        "churn": previsao,
        "probabilidade": float(probabilidade),
        "threshold": THRESHOLD,
    }