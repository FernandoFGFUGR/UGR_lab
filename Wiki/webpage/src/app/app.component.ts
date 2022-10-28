import { Component } from '@angular/core';
import { AngularFireAuth } from '@angular/fire/compat/auth';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {

  usuario!: firebase.default.User
  cargando: boolean = true;
  
  constructor(public afAuth: AngularFireAuth) {
    this.afAuth.user.subscribe((usuario) => {
      console.log(usuario)
      setTimeout(() => {
        this.cargando = false;
        this.usuario = usuario!
      }, 3000);
    })
  }

}