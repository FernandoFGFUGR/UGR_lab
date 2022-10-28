import { Component, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  cookie_value: string = ''
  showCookieMessage!: boolean;

  constructor (
    private cookieSvc: CookieService
  ) 
  {}

  ngOnInit(): void {
    this.cookie_value = this.cookieSvc.get('Neutrino_Cookie')
    this.showCookieMessage = this.cookie_value != '' ? false : true;
    console.log(this.showCookieMessage)
  }

  acceptCookies() {
    this.showCookieMessage = false;
    this.cookieSvc.set('Neutrino_Cookie', 'GDPR', { expires: 3 });
  } 

  rejectCookies() {
    this.showCookieMessage = false;
    this.cookieSvc.delete('Neutrino_Cookie');
  }

}
