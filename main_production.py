import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import warnings
import firebase_admin
warnings.filterwarnings('ignore')

def create_document(collection_name: str, item: dict):
    
    collection_ref = db.collection(collection_name)

    try:
        doc_ref = collection_ref.add(item)
        return True
    
    except:
        return False


firebase_credentials = dict(st.secrets["firebase"]['my_project_settings'])

#################################################################
# Verifique se já existe um app inicializado
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)

# Conectar ao Firestore
db = firestore.client()
################################################################

# Função para carregar e exibir o CSV
def load_data(uploaded_file):
    
    pandas_dataframe = pd.read_csv(uploaded_file) 
    
    return pandas_dataframe

# Configuração do Streamlit
# CSS para customizar a cor do título
st.markdown(
    """
    <style>
    .red-title {
        color: red;
        font-size: 2.5em;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Exibe o título com a cor customizada
st.markdown('<h1 class="red-title">Cadastro de Empresas Ciatos CRM</h1>', unsafe_allow_html=True)
st.write("Faça upload de um arquivo CSV importar dados para o CRM")

# Upload do arquivo CSV
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=["csv"], key="uploaded_file") 

if uploaded_file is not None:
    # Carrega o CSV em um DataFrame
    df = load_data(uploaded_file)
    
    columns_updated = df.columns.to_list()
    
    st.header("Selecione as colunas que deseja importar para a base do Ciatos CRM:")
    
    option_nome_empresa = st.selectbox(
    "Coluna Nome da Empresa",
    columns_updated,placeholder="Selecione a coluna que deseja importar para Nome da Empresa", index=None)

    if option_nome_empresa:
        option_telefone = st.selectbox("Coluna Telefone",columns_updated,placeholder="Selecione a coluna que deseja importar para Telefone", index=None)

        if option_telefone:
            
            if st.button("Importar cadastro para Ciatos CRM"):
                
                coluna_empresa = df[option_nome_empresa].to_list()
                coluna_telefone = df[option_telefone].to_list()

                register_list = [{'empresa': empresa,
                                  'telefone': telefone} for empresa, telefone in zip(coluna_empresa, coluna_telefone)]
                
                [create_document('colecao_documentos', documento) for documento in register_list]

                st.warning("Importação concluída!")
                

        
                
    
    
        
else:
    st.write("Por favor, faça o upload de um arquivo CSV.")
