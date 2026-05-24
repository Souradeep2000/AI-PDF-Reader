import {
  Component,
  ElementRef,
  NgZone,
  signal,
  ViewChild,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { ChatApiService } from '../../core/services/chat-api.service';

interface Message {
  role: 'user' | 'ai';
  content: string;
  timestamp: Date;
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.component.html',
})
export class ChatComponent {
  constructor(
    private chatApi: ChatApiService,
    private ngZone: NgZone,
  ) {}

  messages = signal<Message[]>([
    {
      role: 'ai',
      content: 'Hi! Ask me anything about your studies 👋',
      timestamp: new Date(),
    },
  ]);

  inputText = '';
  isLoading = false;

  @ViewChild('chatContainer')
  chatContainer!: ElementRef;

  async sendMessage() {
    if (!this.inputText.trim()) return;

    const userQuery = this.inputText;
    this.inputText = '';
    this.isLoading = true;

    this.messages.update((msgs) => [
      ...msgs,
      { role: 'user', content: userQuery, timestamp: new Date() },
      { role: 'ai', content: '', timestamp: new Date() },
    ]);

    this.scrollToBottom();

    try {
      const finalData = await this.chatApi.streamAsk(userQuery, 5, (token) => {
        this.messages.update((msgs) => {
          const updated = [...msgs];
          const lastIdx = updated.length - 1;

          if (updated[lastIdx] && updated[lastIdx].role === 'ai') {
            updated[lastIdx] = {
              ...updated[lastIdx],
              content: updated[lastIdx].content + token,
            };
          }
          return updated;
        });
        this.scrollToBottom();
      });

      if (finalData && finalData.answer) {
        this.messages.update((msgs) => {
          const updated = [...msgs];
          const lastIdx = updated.length - 1;

          if (updated[lastIdx] && updated[lastIdx].role === 'ai') {
            // Only overwrite if the real-time stream failed to fetch text tokens
            if (updated[lastIdx].content.trim().length === 0) {
              updated[lastIdx] = {
                ...updated[lastIdx],
                content: finalData.answer,
              };
            }
          }
          return updated;
        });
      }
    } catch (error) {
      console.error(error);
      this.messages.update((msgs) => {
        const updated = [...msgs];
        updated[updated.length - 1].content = 'Something went wrong.';
        return updated;
      });
    } finally {
      this.isLoading = false;
      this.scrollToBottom();
    }
  }

  scrollToBottom() {
    setTimeout(() => {
      this.chatContainer?.nativeElement.scrollTo({
        top: this.chatContainer.nativeElement.scrollHeight,
        behavior: 'smooth',
      });
    }, 50);
  }
}
