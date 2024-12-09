import { Component, OnInit } from '@angular/core';
import { PaymentService } from '../../../service/payment.service';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-payment-list',
  imports: [ FormsModule, HttpClientModule ],
  // providers: [ PaymentService ],
  templateUrl: './payment-list.component.html',
  styleUrls: ['./payment-list.component.css']
})
export class PaymentListComponent implements OnInit {
  payments: any[] = [];
  searchQuery: string = '';

  constructor(private paymentService: PaymentService) {}

  ngOnInit(): void {
    this.fetchPayments();
  }

  fetchPayments(): void {
    this.paymentService.getPayments(0, 10, this.searchQuery).subscribe((data) => {
      this.payments = data;
    });
  }

  onSearch(): void {
    this.fetchPayments();
  }

  deletePayment(paymentId: string): void {
    this.paymentService.deletePayment(paymentId).subscribe(() => {
      // Refresh the list after deletionthis.fetchPayments();
    });
  }

  downloadEvidence(paymentId: string): void {
    const payment = this.payments.find(p => p._id === paymentId);
    if (payment?.evidence_file_id) {
      window.location.href = `http://localhost:8000/payment/download/${paymentId}`;
    } else {
      alert("No evidence file found.");
    }
  }
}