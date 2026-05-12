import { Component, EventEmitter, Output } from '@angular/core';
import { ThemeToggleComponent } from '../theme-toggle/theme-toggle.component';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [ThemeToggleComponent],
  templateUrl: './navbar.component.html',
})
export class NavbarComponent {
  @Output() menuClick = new EventEmitter<void>();
}
