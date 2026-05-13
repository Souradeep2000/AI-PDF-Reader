import { Component, EventEmitter, Output } from '@angular/core';

interface StudyFile {
  id: string;
  name: string;
  type: string;
  status: 'uploaded' | 'processing' | 'ready';
}

@Component({
  selector: 'app-upload-zone',
  imports: [],
  templateUrl: './upload-zone.component.html',
  styleUrl: './upload-zone.component.css',
})
export class UploadZoneComponent {
  @Output() uploadCompleted = new EventEmitter<StudyFile[]>();

  uploadedFiles: StudyFile[] = [];

  handleUpload(fileList: FileList) {
    const files = Array.from(fileList);

    files.forEach((file, index) => {
      const newFile: StudyFile = {
        id: Math.random().toString(36).substring(2),
        name: file.name,
        type: file.name.split('.').pop() || 'file',
        status: 'uploaded',
      };

      this.uploadedFiles.push(newFile);

      setTimeout(() => {
        newFile.status = 'processing';

        setTimeout(() => {
          newFile.status = 'ready';

          // Trigger only once after first file ready
          if (index === 0) {
            this.uploadCompleted.emit(this.uploadedFiles);
          }
        }, 1200);
      }, 500);
    });
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;

    if (input.files?.length) {
      this.handleUpload(input.files);
    }
  }
}
