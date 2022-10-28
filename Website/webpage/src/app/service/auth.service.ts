import { Injectable } from '@angular/core';
import { AngularFireAuth } from '@angular/fire/compat/auth';


@Injectable()
export class AuthService {

  usuario!: firebase.default.User

  constructor(
    public afAuth: AngularFireAuth) 
  { }

  async login(email: string, password: string) { 
    try {
      return await this.afAuth.signInWithEmailAndPassword(email, password)
    } catch(error) {
      console.log(error)
      return "error"
    }
  }

  async logout() {
    try {
      return await this.afAuth.signOut()
    } catch(error) {
      console.log(error)
      return "error"
    }
  }

  async resetPassword(email: string):Promise<void> {
    try {
      return this.afAuth.sendPasswordResetEmail(email)
    } catch(error) {
      console.log(error)
    }
  }

}