import { Component, OnInit } from '@angular/core';
import { AuthService } from '../service/auth.service'
import { Router } from '@angular/router';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  constructor(
    private authSrv: AuthService, 
    private router: Router
  ) {}

  ngOnInit(): void {
    
  }

  async logoutService() {
    const Toast = Swal.mixin({
      toast: true,
      position: 'bottom-end',
      showConfirmButton: false,
      timer: 3000,
      timerProgressBar: true,
      didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
      }
    })
    try {
      await this.authSrv.logout()
      .then((success) => {
        Toast.fire({
          icon: 'success',
          title: 'La sesión se ha cerrado correctamente'
        })
        setTimeout(() => { 
          this.router.navigate(['/login'])
        }, 1000);
      })  
    } catch(error) {
      console.log(error)
    }

  }

}