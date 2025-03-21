import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-form',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './form.component.html',
  styleUrl: './form.component.css'
})
export class FormComponent {

  modo: 'codificar' | 'decodificar' | null = null; // Propiedad para rastrear la opción seleccionada

  constructor() { }

  seleccionarModo(modo: 'codificar' | 'decodificar') {
    this.modo = modo; // Actualiza el modo seleccionado
  }

}
