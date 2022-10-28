import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ComponenteComponent } from './componente/componente.component';
import { ContactComponent } from './contact/contact.component';
import { CookiesComponent } from './cookies/cookies.component';
import { ErrorComponent } from './error/error.component';
import { HomeComponent } from './home/home.component';
import { LegalComponent } from './legal/legal.component';
import { LoginComponent } from './login/login.component';
import { MembersComponent } from './members/members.component';
import { NewsComponent } from './news/news.component';
import { PrivacyComponent } from './privacy/privacy.component';
import { PublicationsComponent } from './publications/publications.component';
import { ResearchComponent } from './research/research.component';
import { ResetComponent } from './reset/reset.component';
import { TalksComponent } from './talks/talks.component';
import { ThesisComponent } from './thesis/thesis.component';

const routes: Routes = [
  {
    path: '', component: HomeComponent
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
    path: 'research', component: ResearchComponent
  },
  {
    path: 'news', component: NewsComponent
  },
  {
    path: 'publications', component: PublicationsComponent
  },
  {
    path: 'talks', component: TalksComponent
  },
  {
    path: 'thesis', component: ThesisComponent
  },
  {
    path: 'members', component: MembersComponent
  },
  {
    path: 'contact', component: ContactComponent
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
