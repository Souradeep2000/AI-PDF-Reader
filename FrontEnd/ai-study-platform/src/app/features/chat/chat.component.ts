import { Component, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface Message {
  role: 'user' | 'ai';
  content: string;
  timestamp: Date;
}

@Component({
  selector: 'app-chat',
  imports: [FormsModule, CommonModule],
  templateUrl: './chat.component.html',
})
export class ChatComponent {
  messages: Message[] = [
    {
      role: 'ai',
      content: 'Hi! Ask me anything about your studies 👋',
      timestamp: new Date(),
    },
  ];

  inputText = '';
  isLoading = false;

  @ViewChild('chatContainer') chatContainer!: ElementRef;

  sendMessage() {
    if (!this.inputText.trim()) return;

    // push user message
    this.messages.push({
      role: 'user',
      content: this.inputText,
      timestamp: new Date(),
    });

    const userQuery = this.inputText;
    this.inputText = '';

    this.scrollToBottom();

    // fake AI response (replace later with FastAPI)
    this.isLoading = true;

    setTimeout(() => {
      this.messages.push({
        role: 'ai',
        content: `You said: "${userQuery}". (AI response placeholder)`,
        timestamp: new Date(),
      });

      this.isLoading = false;
      this.scrollToBottom();
    }, 800);
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
