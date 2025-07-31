def gerar_nova_senha():
    consoantes = list("bcdfghjklmnpqrstvwxyz")
    numeros = list("123456789")
    password = "".join(random.choices(consoantes, k=4)) + "".join(random.choices(numeros, k=4))
    return password
    

if __name__ == "__main__":
    import random
    # from time import sleep
    # from app.tools import escrever, tecla, get_tela_atual, enviar_email, update_env_variable

    # intervalo_teclas = 100  # Intervalo entre teclas em milissegundos
    # usuario = "admin"
    # email_admin = "
    print(gerar_nova_senha())
    
    wxrk2737