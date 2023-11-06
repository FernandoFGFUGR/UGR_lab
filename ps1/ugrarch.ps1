# Importar el módulo WinSCP
Add-Type -Path "C:\Program Files (x86)\WinSCP\WinSCPnet.dll"

# Configurar la sesión de conexión a SFTP
$sessionOptions = New-Object WinSCP.SessionOptions
$sessionOptions.Protocol = [WinSCP.Protocol]::Sftp
$sessionOptions.HostName = "192.168.0.2"
$sessionOptions.UserName = "arch-guest"
$sessionOptions.Password = "arch-guest"
$sessionOptions.SshHostKeyFingerprint = "ssh-rsa 2048 Wdajn7XKu2Fsbbx3xorcUiMoB+Qbi+GdYPDMGt5w6hk"


# Iniciar la sesión de WinSCP
$session = New-Object WinSCP.Session
$session.Open($sessionOptions)

# Especificar la carpeta remota y local
$remotePath = "/home/ferfuentguerr/Programacion/ugrarch/ova"
$localPath = "C:\Users\Usuario\Desktop"

# Enviar el archivo al servidor remoto
$transferOptions = New-Object WinSCP.TransferOptions
$transferResult = $session.GetFiles($remotePath, $localPath, $False, $transferOptions)

# Comprobar si ha ocurrido algún error en la transferencia
if ($transferResult.IsSuccess)
{
    Write-Host "Ugrarch ha sido recibido correctamente."
}
else
{
    Write-Host "Ha ocurrido un error al transferir el archivo:" $transferResult.Failures[0].Message
}

# Cerrar la sesión de WinSCP
$session.Dispose()

Read-Host -Prompt "Presione Enter para salir"