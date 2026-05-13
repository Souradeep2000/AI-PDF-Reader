import { Component, EventEmitter, Input, Output } from '@angular/core';
import { ChatStateService } from '../../../core/services/chat-state.service';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  templateUrl: './sidebar.component.html',
})
export class SidebarComponent {
  @Input() isOpen = false;

  @Output()
  closeSidebar = new EventEmitter<void>();

  constructor(public chatState: ChatStateService) {}
}
