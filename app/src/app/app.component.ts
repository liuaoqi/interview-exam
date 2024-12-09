import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FormsModule,ReactiveFormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { PaymentListComponent } from './components/payment-list/payment-list.component';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet,MatCardModule,FormsModule,ReactiveFormsModule,PaymentListComponent, HttpClientModule ],
  providers: [  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})

export class AppComponent {
  title = 'angular';

  tasks:any=[];

  // APIURL="http://127.0.0.1:8000/";


}
