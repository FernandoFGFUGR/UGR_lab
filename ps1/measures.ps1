# Importar el módulo WinSCP
Add-Type -Path "C:\Program Files (x86)\WinSCP\WinSCPnet.dll"

# Configurar la sesión de conexión a SFTP
$sessionOptions = New-Object WinSCP.SessionOptions
$sessionOptions.Protocol = [WinSCP.Protocol]::Sftp
$sessionOptions.HostName = "150.214.24.215"
$sessionOptions.UserName = "root"
$sessionOptions.Password = "SiPMUGR128"
$sessionOptions.SshHostKeyFingerprint = "ssh-rsa 2048 Wdajn7XKu2Fsbbx3xorcUiMoB+Qbi+GdYPDMGt5w6hk"


# Iniciar la sesión de WinSCP
$session = New-Object WinSCP.Session
$session.Open($sessionOptions)

# Obtener la ruta completa del archivo seleccionado
$filePath = $args[0]

# Enviar el archivo al servidor remoto
$transferOptions = New-Object WinSCP.TransferOptions
$transferResult = $session.PutFiles($filePath, "/home/MassiveTestMeasures/"+$args[0].Name, $False, $transferOptions)

# Comprobar si ha ocurrido algún error en la transferencia
if ($transferResult.IsSuccess)
{
    Write-Host "Medida guardada correctamente."
}
else
{
    Write-Host "Ha ocurrido un error al transferir el archivo al servidor:" $transferResult.Failures[0].Message
}

# Cerrar la sesión de WinSCP
$session.Dispose()

Read-Host -Prompt "Presione Enter para salir"