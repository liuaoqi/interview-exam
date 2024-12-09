import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class PaymentService {
  private apiUrl = 'http://localhost:8000/payment/';

  constructor(private http: HttpClient) {}

  getPayments(skip: number = 0, limit: number = 10, search: string = ''): Observable<any> {
    let params = new HttpParams().set('skip', skip.toString()).set('limit', limit.toString());
    if (search) {
      params = params.set('search', search);
    }

    return this.http.get(this.apiUrl, { params });
  }

  createPayment(paymentData: any): Observable<any> {
    return this.http.post(this.apiUrl, paymentData);
  }

  updatePayment(paymentId: string, paymentData: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${paymentId}`, paymentData);
  }

  deletePayment(paymentId: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${paymentId}`);
  }

  uploadEvidence(paymentId: string, file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file, file.name);
    return this.http.post(`${this.apiUrl}/${paymentId}/upload_evidence`, formData);
  }

  // Method to download the evidence file
  downloadEvidence(paymentId: string) {
    this.http.get(`${this.apiUrl}/download/${paymentId}`, {
      responseType: 'blob'  // This will receive the file content as Blob (binary data)
    }).subscribe((response: Blob) => {
      // Create a URL for the Blob object (i.e., the binary data)
      const downloadLink = document.createElement('a');
      const url = window.URL.createObjectURL(response);
      downloadLink.href = url;
      downloadLink.download = 'evidence.pdf'; // Set the desired filename

      // Trigger the download by simulating a click
      downloadLink.click();

      // Clean up the URL object after the download
      window.URL.revokeObjectURL(url);
    }, (error) => {
      console.error('Error downloading evidence:', error);
    });
  }
}
