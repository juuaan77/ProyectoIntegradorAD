__author__ = 'juan'

import commands
from bottle import Bottle,route,run,request,get


#El siguiente codigo crea maquinas virtuales, al mismo se accede a travez de una interfaz web que
#provee cuadros de texto donde se ingresan las especificaciones deseadas paras las VMs
#asi mismo, el "duenio" de los archivos creados con este codigo es el usuario que lo ejecuta
#para asi permitir que se pueda acceder a el via we.

@route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>'''

@route('/login',method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if username=="root" and password=="root":
        return datosvm()

    else:
        return "<p>Login failed.</p>"

@route('/datosvm')
def datosvm():
    salida = commands.getstatusoutput('cat /home/juan/Proyecto\ integrador/repositorio/HTML/FdatosVMSVMithKVMweb.html')
    return ''''''+salida[1]

@route('/datosvm',method='POST')
def do_datosvm():

    nombre = request.forms.get('nombre')
    so = request.forms.get('so')
    memoria = request.forms.get('memoria')
    disco = request.forms.get('disco')
    interfaz = request.forms.get('interfaz')
    direccion = request.forms.get('direccion')

    parte1 = "La maquina virtula sera creada con el nombre " + nombre + " para hostear el sistema operativo " + so
    parte2 = parte1 + " con la memoria " + memoria + " y el disco " + disco + " y utilizara la interfaz " + interfaz
    parte3 = parte2 + " como bridge"
    #return parte3
    return crearvm(nombre,so,memoria,disco,interfaz,direccion)

def crearvm(nombre,so,memoria,disco,interfaz,direccion):
    #commands.getstatusoutput('touch /home/juan/ojalaqueeste')
    usuario = commands.getstatusoutput('whoami')
    #print salida[1]
    #mkdir /home/juan/VirtualBox\ VMs/prueba
    ruta =  'mkdir '+ direccion + '/' + nombre + "\n"
    salida = commands.getstatusoutput('mkdir '+ direccion + '/' + nombre)
    print salida[1]

    comando = 'virt-install  --connect qemu:///system --virt-type kvm --name ' + nombre + ' --ram ' + memoria + ' --disk path=/home/juan/KVMs/'+nombre+'/'+nombre+'.img,size=' + disco + ' --network bridge=' + interfaz + ' --graphics vnc --boot network=on --os-type linux --os-variant ' + so + ' --noreboot'
    salida = commands.getstatusoutput(comando)
    print salida[1]
    return '''La maquina fue creada con exito''' + datosvm()

run(host='localhost', port=8080)