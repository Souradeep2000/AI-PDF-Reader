import { Component, EventEmitter, Output, signal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UploadService } from '../../../core/services/upload.service';

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

  private uploadService = inject(UploadService);
  uploadedFiles: StudyFile[] = [];

  isUploading = signal(false);
  uploadProgress = signal(0);
  processingStatus = signal<'uploading' | 'processing'>('uploading');

  private processingInterval: any;

  handleUpload(fileList: FileList) {
    const files = Array.from(fileList);
    if (!files.length) return;

    const fileToUpload = files[0];

    this.isUploading.set(true);
    this.uploadProgress.set(0);
    this.processingStatus.set('uploading');
    this.clearProcessingInterval();

    this.uploadService.uploadSingleFile(fileToUpload).subscribe({
      next: (event) => {
        if (event.type === 'progress') {
          const networkProgress = Math.round((event.value * 80) / 100);

          if (
            networkProgress > this.uploadProgress() &&
            this.processingStatus() === 'uploading'
          ) {
            this.uploadProgress.set(networkProgress);
          }

          // Once network payload completes, smoothly hand off to AI simulations
          if (event.value >= 100 && this.processingStatus() === 'uploading') {
            this.startAiProcessingSimulation();
          }
        } else if (event.type === 'done') {
          // Backend complete! Snap directly to completion
          this.clearProcessingInterval();
          this.uploadProgress.set(100);

          const backendData = event.value;
          const newFile: StudyFile = {
            id:
              backendData.document_id ||
              Math.random().toString(36).substring(2),
            name: fileToUpload.name,
            type:
              backendData.file_type ||
              fileToUpload.name.split('.').pop() ||
              'file',
            status: 'ready',
          };

          this.uploadedFiles.push(newFile);

          setTimeout(() => {
            this.isUploading.set(false);
            this.uploadCompleted.emit();
          }, 600);
        }
      },
      error: (err) => {
        console.error('Upload failed:', err);
        this.cleanupState();
      },
    });
  }

  private startAiProcessingSimulation() {
    this.processingStatus.set('processing');

    if (this.uploadProgress() < 80) {
      this.uploadProgress.set(80);
    }

    // Tick up slowly from 80% towards 99% while backend runs embedding pipelines
    this.processingInterval = setInterval(() => {
      const current = this.uploadProgress();
      if (current < 95) {
        this.uploadProgress.update((v) => v + 2); // Tick by 2s below 95%
      } else if (current < 99) {
        this.uploadProgress.update((v) => v + 1); // Slow down significantly right before completion
      }
    }, 450);
  }

  private clearProcessingInterval() {
    if (this.processingInterval) {
      clearInterval(this.processingInterval);
    }
  }

  private cleanupState() {
    this.clearProcessingInterval();
    this.isUploading.set(false);
    this.uploadProgress.set(0);
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files?.length) {
      this.handleUpload(input.files);
    }
  }
}
