import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { NavbarComponent } from './shared/components/navbar/navbar.component';
import { SidebarComponent } from './shared/components/sidebar/sidebar.component';
import { ChatStateService } from './core/services/chat-state.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent, SidebarComponent],
  templateUrl: './app.component.html',
})
export class AppComponent {
  isSidebarOpen = signal(false);

  constructor(public chatState: ChatStateService) {}

  toggleSidebar() {
    this.isSidebarOpen.update((v) => !v);
  }

  closeChat() {
    this.chatState.closeChat();
  }
}
