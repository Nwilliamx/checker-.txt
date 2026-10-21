
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client

BASE_DIR = Path(__file__).resolve().parent
WORDLIST = BASE_DIR / "senhas.txt"

INTERVALO = 2.1
MAX_TENTATIVAS = 300

load_dotenv(BASE_DIR / ".env")

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_PUBLISHABLE_KEY")

if not url or not key:
    raise SystemExit(
        "Configure SUPABASE_URL e SUPABASE_PUBLISHABLE_KEY no .env"
    )

if not WORDLIST.is_file():
    raise SystemExit(f"Arquivo não encontrado: {WORDLIST}")

email = input("E-mail da conta de teste: ").strip()

if not email:
    raise SystemExit("O e-mail não pode estar vazio.")

confirmacao = input(
    "Confirme que é sua conta de teste digitando TESTE: "
).strip()

if confirmacao != "TESTE":
    raise SystemExit("Teste cancelado.")

with WORDLIST.open("r", encoding="utf-8") as arquivo:
    senhas = [
        linha.rstrip("\r\n")
        for linha in arquivo
        if linha.rstrip("\r\n")
    ]

senhas = senhas[:MAX_TENTATIVAS]

if not senhas:
    raise SystemExit("O arquivo senhas.txt está vazio.")

supabase = create_client(url, key)

print(f"\nCandidatos carregados: {len(senhas)}")
print("Iniciando o teste controlado...\n")

inicio = time.perf_counter()
encontrada = False

for numero, senha in enumerate(senhas, start=1):
    print(f"Tentativa {numero}/{len(senhas)}")

    try:
        resultado = supabase.auth.sign_in_with_password({
            "email": email,
            "password": senha,
        })

        if resultado.user and resultado.session:
            duracao = time.perf_counter() - inicio
            print("\nLogin aceito.")
            print(f"Senha correspondente: {senha}")
            print(f"Tentativas: {numero}")
            print(f"Tempo: {duracao:.2f} segundos")
            encontrada = True

            supabase.auth.sign_out()
            break

        print("A autenticação não retornou uma sessão.")
        break

    except Exception as erro:
        status = getattr(erro, "status", None)
        codigo = getattr(erro, "code", None)
        mensagem = str(erro)
        mensagem_lower = mensagem.lower()

        # Só continua quando a API identifica credenciais inválidas.
        credenciais_invalidas = (
            status == 400
            and (
                codigo == "invalid_credentials"
                or "invalid login credentials" in mensagem_lower
            )
        )

        if credenciais_invalidas:
            if numero < len(senhas):
                time.sleep(INTERVALO)
            continue

        # Não tenta contornar bloqueios ou erros inesperados.
        print("\nTeste interrompido.")
        print(f"HTTP status: {status}")
        print(f"Código: {codigo}")
        print(f"Detalhes: {mensagem}")
        print("Verifique a configuração ou aguarde se houver limite.")
        break

if not encontrada:
    print("\nNenhuma autenticação bem-sucedida foi confirmada.")

duracao = time.perf_counter() - inicio
print(f"Tempo total: {duracao:.2f} segundos")