import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ComponenteComponent } from './componente/componente.component';
import { CookiesComponent } from './cookies/cookies.component';
import { ErrorComponent } from './error/error.component';
import { HomeComponent } from './home/home.component';
import { LegalComponent } from './legal/legal.component';
import { LoginComponent } from './login/login.component';
import { PrivacyComponent } from './privacy/privacy.component';
import { ResetComponent } from './reset/reset.component';

const routes: Routes = [
  {
    path: '', component: LoginComponent
  },
  {
    path: 'reset', component: ResetComponent
  },
  {
    path: 'login', component: LoginComponent
  },
  {
    path: 'componente', component: ComponenteComponent
  },
  {
    path: 'privacy', component: PrivacyComponent
  },
  {
    path: 'legal', component: LegalComponent
  },
  {
    path: 'cookies', component: CookiesComponent
  },
  {
    path: '**', component: ErrorComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
