import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PaymentListComponent } from './components/payment-list/payment-list.component';
import { AddPaymentComponent } from './components/add-payment/add-payment.component';

export const routes: Routes = [
  { path: '', component: PaymentListComponent },
  { path: 'add-payment', component: AddPaymentComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
