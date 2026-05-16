import { Component, EventEmitter, Input, Output } from '@angular/core';
import { ThemeToggleComponent } from '../theme-toggle/theme-toggle.component';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [ThemeToggleComponent],
  templateUrl: './navbar.component.html',
})
export class NavbarComponent {
  @Output() menuClick = new EventEmitter<void>();
  @Input() showChat = false;
  @Output() closeChat = new EventEmitter<void>();
}
