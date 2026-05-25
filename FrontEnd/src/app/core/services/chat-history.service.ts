import { Injectable, signal } from '@angular/core';

export interface Message {
  role: 'user' | 'ai';
  content: string;
  timestamp: Date;
}

export interface ChatSession {
  id: string;
  title: string;
  createdAt: string;
  updatedAt: string;
  messages: Message[];
}

@Injectable({
  providedIn: 'root',
})
export class ChatHistoryService {
  private STORAGE_KEY = 'study_ai_chats';

  recentChats = signal<ChatSession[]>(this.loadChats());

  currentChatId = signal<string | null>(null);

  private loadChats(): ChatSession[] {
    const data = localStorage.getItem(this.STORAGE_KEY);

    return data ? JSON.parse(data) : [];
  }

  private saveChats(chats: ChatSession[]) {
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(chats));

    this.recentChats.set(chats);
  }

  createNewChat() {
    const newChat: ChatSession = {
      id: crypto.randomUUID(),
      title: 'New Chat',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      messages: [],
    };

    const updatedChats = [newChat, ...this.recentChats()].slice(0, 20);

    this.saveChats(updatedChats);
    this.currentChatId.set(newChat.id);
  }

  openChat(chatId: string) {
    this.currentChatId.set(chatId);
  }

  getCurrentChat(): ChatSession | null {
    const chatId = this.currentChatId();

    if (!chatId) return null;

    return this.recentChats().find((chat) => chat.id === chatId) || null;
  }

  saveMessage(message: Message) {
    const chatId = this.currentChatId();

    if (!chatId) return;

    const updatedChats = this.recentChats().map((chat) => {
      if (chat.id !== chatId) {
        return chat;
      }

      const updatedMessages = [...chat.messages, message].slice(-20);

      let title = chat.title;

      if (title === 'New Chat' && message.role === 'user') {
        title =
          message.content.length > 30
            ? message.content.slice(0, 30) + '...'
            : message.content;
      }

      return {
        ...chat,
        title,
        updatedAt: new Date().toISOString(),
        messages: updatedMessages,
      };
    });

    this.saveChats(updatedChats);
  }
}
