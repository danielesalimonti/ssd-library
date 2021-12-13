import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import {AuthService} from "../../services/auth.service";
import {AlertController, ToastController} from "@ionic/angular";

@Component({
  selector: 'app-error-page',
  templateUrl: './error-page.page.html',
  styleUrls: ['./error-page.page.scss'],
})
export class ErrorPagePage implements OnInit {

  status: string;
  message: string;

  constructor(private router: Router,
              private auth: AuthService,
              private toastController: ToastController) {

    if(!this.auth.isLogged()) {
      this.router.navigate(['/login']);
    }

    const e: string = localStorage.getItem('error');

    if(e === null || e === undefined || e === '') {
      this.router.navigate(['/home']);
    }else{
      const json = JSON.parse(e);

      this.status = json.status;
      this.message = json.message;

      localStorage.removeItem('error');
    }
  }

  ngOnInit() {
  }

  logout(){
    this.auth.logout().subscribe(
      data => this.router.navigate(['/login']),
      error => this.createToast(error)
    );
  }

  async createToast(error){
    if(error.status === 0){
      error.error.detail = 'Lost Connection';
    }

    const toast = await this.toastController.create({
      header: 'Error ',
      message: error.error.detail,
      position: 'top',
      duration: 5000,
      buttons:[
        {
          text: 'X',
          role: 'cancel'
        }
      ]
    });
    await toast.present();
  }
}
