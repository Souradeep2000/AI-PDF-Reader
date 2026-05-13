import { CommonModule } from '@angular/common';
import { Component, Input, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { UploadZoneComponent } from '../../shared/components/upload-zone/upload-zone.component';
import { ChatComponent } from '../chat/chat.component';
import { ChatStateService } from '../../core/services/chat-state.service';

@Component({
  selector: 'app-home',
  imports: [CommonModule, FormsModule, UploadZoneComponent, ChatComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
})
export class HomeComponent {
  constructor(public chatState: ChatStateService) {}
  isChatOpen = signal(false);

  onUploadCompleted() {
    this.chatState.openChat();
  }
}
