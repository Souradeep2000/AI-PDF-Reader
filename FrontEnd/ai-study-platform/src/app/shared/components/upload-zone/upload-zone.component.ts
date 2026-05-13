import { Component, EventEmitter, Output, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

interface StudyFile {
  id: string;
  name: string;
  type: string;
  status: 'uploaded' | 'processing' | 'ready';
}

@Component({
  selector: 'app-upload-zone',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './upload-zone.component.html',
  styleUrl: './upload-zone.component.css',
})
export class UploadZoneComponent {
  @Output() uploadCompleted = new EventEmitter<void>();

  uploadedFiles: StudyFile[] = [];

  isUploading = signal(false);
  uploadProgress = signal(0);

  handleUpload(fileList: FileList) {
    const files = Array.from(fileList);

    if (!files.length) return;

    this.isUploading.set(true);
    this.uploadProgress.set(0);

    // Fake premium upload animation
    const interval = setInterval(() => {
      const current = this.uploadProgress();

      if (current >= 100) {
        clearInterval(interval);

        files.forEach((file) => {
          const newFile: StudyFile = {
            id: Math.random().toString(36).substring(2),
            name: file.name,
            type: file.name.split('.').pop() || 'file',
            status: 'ready',
          };

          this.uploadedFiles.push(newFile);
        });

        setTimeout(() => {
          this.isUploading.set(false);
          this.uploadCompleted.emit();
        }, 400);

        return;
      }

      this.uploadProgress.update((v) => v + 4);
    }, 80);
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;

    if (input.files?.length) {
      this.handleUpload(input.files);
    }
  }
}
