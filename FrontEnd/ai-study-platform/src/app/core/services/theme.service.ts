import { Injectable, signal } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ThemeService {
  isDarkMode = signal(true);

  constructor() {
    const savedTheme = localStorage.getItem('theme');

    if (savedTheme === 'light') {
      this.enableLightMode();
    } else {
      this.enableDarkMode();
    }
  }

  toggleTheme() {
    this.isDarkMode() ? this.enableLightMode() : this.enableDarkMode();
  }

  enableDarkMode() {
    document.documentElement.classList.add('dark');

    localStorage.setItem('theme', 'dark');

    this.isDarkMode.set(true);
  }

  enableLightMode() {
    document.documentElement.classList.remove('dark');

    localStorage.setItem('theme', 'light');

    this.isDarkMode.set(false);
  }
}
