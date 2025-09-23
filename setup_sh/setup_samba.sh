#!/bin/bash

# ==============================================================================
# Script de Configuração Automática do Servidor Samba
# ==============================================================================

# -- VERIFICA SE O SCRIPT ESTÁ SENDO EXECUTADO COMO ROOT --
if [ "$EUID" -ne 0 ]; then
  echo "Por favor, execute este script como root ou com sudo."
  exit
fi

# -- VARIÁVEIS DE SENHA --
# ATENÇÃO: Hardcodar senhas em scripts é uma má prática de segurança em produção.
# Para um laboratório, é aceitável. Em um ambiente real, use variáveis de ambiente
# ou um sistema de gerenciamento de segredos (como o Vault).
ZEUS_PASS="zeus123"
HERMES_PASS="hermes123"
HADES_PASS="hades123"

echo ">>> Iniciando a configuração do servidor Samba..."

# 1. ATUALIZAÇÃO E INSTALAÇÃO DE PACOTES
echo "--> Atualizando o sistema e instalando o Samba..."
apt-get update > /dev/null 2>&1
apt-get install samba -y

# 2. CRIAÇÃO DE GRUPOS E USUÁRIOS
echo "--> Criando grupos: samba_admins, samba_editors, samba_readers..."
addgroup --quiet samba_admins
addgroup --quiet samba_editors
addgroup --quiet samba_readers

echo "--> Criando usuários: zeus, hermes, hades..."
useradd -m -g samba_admins -s /bin/bash zeus
useradd -m -g samba_editors -s /bin/bash hermes
useradd -m -g samba_readers -s /bin/bash hades

# 3. CONFIGURAÇÃO DAS SENHAS DO SAMBA (DE FORMA NÃO INTERATIVA)
echo "--> Configurando senhas do Samba..."
(echo "$ZEUS_PASS"; echo "$ZEUS_PASS") | smbpasswd -a -s zeus
(echo "$HERMES_PASS"; echo "$HERMES_PASS") | smbpasswd -a -s hermes
(echo "$HADES_PASS"; echo "$HADES_PASS") | smbpasswd -a -s hades

smbpasswd -e zeus
smbpasswd -e hermes
smbpasswd -e hades

# 4. CRIAÇÃO DA ESTRUTURA DE DIRETÓRIOS
echo "--> Criando a estrutura de diretórios em /srv/samba/dados..."
mkdir -p /srv/samba/dados/Projetos
mkdir -p /srv/samba/dados/Arquivos

# 5. APLICAÇÃO DAS PERMISSÕES NO SISTEMA DE ARQUIVOS
echo "--> Aplicando permissões na pasta Projetos..."
chgrp samba_editors /srv/samba/dados/Projetos
chmod 2770 /srv/samba/dados/Projetos
chmod +t /srv/samba/dados/Projetos

echo "--> Aplicando permissões na pasta Arquivos..."
chgrp samba_readers /srv/samba/dados/Arquivos
chmod 750 /srv/samba/dados/Arquivos

# 6. CONFIGURAÇÃO DO ARQUIVO smb.conf
echo "--> Configurando o /etc/samba/smb.conf..."
# Faz um backup do arquivo original
cp /etc/samba/smb.conf /etc/samba/smb.conf.bak

# Usa um "Here Document" (EOF) para sobrescrever o arquivo com a nova configuração
cat <<EOF > /etc/samba/smb.conf
[global]
   workgroup = WORKGROUP
   server string = %h server (Samba, Ubuntu)
   log file = /var/log/samba/log.%m
   max log size = 1000
   logging = file
   panic action = /usr/share/samba/panic-action %d
   server role = standalone server
   obey pam restrictions = yes
   unix password sync = yes
   passwd program = /usr/bin/passwd %u
   passwd chat = *Enter\snew\s*\spassword:* %n\n *Retype\snew\s*\spassword:* %n\n *password\supdated\ssuccessfully* .
   pam password change = yes
   map to guest = bad user
   usershare allow guests = yes

[Projetos]
    comment = Pasta de colaboracao para Editores
    path = /srv/samba/dados/Projetos
    browseable = yes
    writable = yes
    valid users = @samba_admins, @samba_editors
    force group = samba_editors
    create mask = 0660
    directory mask = 0770

[Arquivos]
    comment = Pasta de leitura para Leitores
    path = /srv/samba/dados/Arquivos
    browseable = yes
    read only = yes
    valid users = @samba_admins, @samba_readers
EOF

# 7. REINICIAR E VERIFICAR OS SERVIÇOS
echo "--> Reiniciando e habilitando os serviços do Samba..."
systemctl restart smbd
systemctl restart nmbd
systemctl enable smbd
systemctl enable nmbd

# 8. CONFIGURAR O FIREWALL (UFW)
echo "--> Configurando o firewall (UFW)..."
ufw allow samba > /dev/null 2>&1

echo ">>> Configuração do Samba concluída com sucesso!"