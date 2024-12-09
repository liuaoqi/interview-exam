import { Component } from '@angular/core';
import { PaymentService } from '../../../service/payment.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-add-payment',
  imports: [ FormsModule ],
  templateUrl: './add-payment.component.html',
  styleUrls: ['./add-payment.component.css']
})
export class AddPaymentComponent {
  paymentData = {
    payee_first_name: '',
    payee_last_name: '',
    payee_email: '',
    payee_phone_number: '',
    payee_address_line_1: '',
    payee_city: '',
    payee_country: '',
    payee_postal_code: '',
    payee_due_date: '',
    due_amount: 0,
    currency: '',
  };
  isSubmitting = false;

  constructor(private paymentService: PaymentService) {}

  onSubmit(): void {
    if (!this.paymentData.payee_first_name || !this.paymentData.payee_last_name || !this.paymentData.payee_email) {
      alert("Please fill in all required fields.");
      return;
    }

    this.isSubmitting = true;
    this.paymentService.createPayment(this.paymentData).subscribe(
      response => {
        this.isSubmitting = false;
        alert("Payment created successfully!");
        // Optionally redirect to the payment list or reset form
      },
      error => {
        this.isSubmitting = false;
        alert("Failed to create payment.");
      }
    );
  }
}
