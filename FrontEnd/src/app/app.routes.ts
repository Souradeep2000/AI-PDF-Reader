import { Routes } from '@angular/router';
import { HomeComponent } from './features/home/home.component';
import { AnalyticsComponent } from './features/analytics/analytics.component';
import { ChatComponent } from './features/chat/chat.component';

export const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
  },
  {
    path: 'analytics',
    component: AnalyticsComponent,
  },
  { path: 'chat', component: ChatComponent },
];
