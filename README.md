# Python Password Checker

Checker local desenvolvido em Python para testar senhas de um arquivo de texto utilizando a API de autenticação do Supabase.

## Requisitos

- Python 3.10 ou superior
- Conexão com a internet
- URL e chave pública do projeto Supabase

## Estrutura do projeto

```text
password_checker/
├── main.py
├── .env
├── senhas.txt
├── requirements.txt
└── README.md
```

## Instalação

Com o Python instalado, abra o terminal na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

Esse comando instala as dependências necessárias para executar o programa.

## Configuração

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
SUPABASE_URL="https://seu-projeto.supabase.co"
SUPABASE_PUBLISHABLE_KEY="sua_chave_publica"
```

Substitua os valores de exemplo pelas informações do projeto que será utilizado nos testes.

## Arquivo de senhas

O arquivo `senhas.txt` deve estar na mesma pasta do programa e conter uma senha por linha.

Exemplo:

```text
senha_de_teste_01
senha_de_teste_02
senha_de_teste_03
```

O programa lê o arquivo e processa as senhas individualmente.

## Como executar

Após configurar as variáveis de ambiente e preparar o arquivo de senhas, execute:

```bash
python main.py
```

Os resultados e as informações da execução serão exibidos no terminal, conforme a implementação do programa.

## Observações

O funcionamento depende da configuração correta das variáveis de ambiente, das dependências instaladas e da disponibilidade do serviço de autenticação.

Utilize a ferramenta somente em projetos próprios ou em ambientes para os quais você tenha autorização. Evite utilizar senhas reais de terceiros e mantenha arquivos com credenciais fora de repositórios públicos. Adicione o `.env` ao `.gitignore` para evitar o envio acidental de configurações locais.
