# servicio_viajes
Aplicación de gestión de servicio de viajes. Haciendo la carga, filtrado, eliminación y modificación de los datos en sql.  
Proyecto Nivel Inicial: 

    La idea de este proyecto es hacer una aplicación encargada de gestionar viajes. Las 

funciones principales que tendrá en esta entrega serán cinco:  

    1. La carga de nuevos viajes (casilla "Carga Viaje"), carga que precisa la entrada  

       por teclado de: origen, destino, fecha y hora de salida, asientos disponibles  

       e id del chofer. 

    2. La visualización de viajes disponibles dentro de la lista "Viajes Disponibles" 

       que se podrá filtrar por origen, destino y fecha de salida (casilla "Filtrar 

       Viajes"). 

    3. La selección y deselección de un viaje. La selección se hará al cliquear en uno  

       uno de los viajes disponibles mostrados en la lista, se podrá visualizar y  

       deseleccionar (usando botón "deseleccionar") el mismo en la casilla "viaje 

       seleccionado". 

    4. La reserva de asientos de un viaje seleccionado, únicamente permitido si hay en 

       disposición la cantidad deseada. 

    5. La eliminación de un viaje. Los viajes son quitados de la lista por tres motivos: 

           I. Que no haya más asientos disponibles 

           II. Que la fecha del viaje sea anterior a la fecha actual, es decir el viaje  

               ya se hizo. 

           III. Que se desee eliminar el viaje por algún motivo. Para esto, se selecciona 

                el viaje a eliminar, utilizando la casilla "Eliminar Viaje" se selecciona 

                el id del chofer y se elimina (botón "eliminar"). 

  

Hasta acá la implementación del proyecto base.  

  

Sobre la idea del Proyecto Completo:  

    Para el proyecto completo la idea es hacer una aplicación de gestión viajes nacionales, 

    pero más completa. Sería una red de usuarios, estos usuarios pueden realizar un viaje 

    y publicarlo, o pueden buscar un viaje y solicitar asiento en el mismo. Al buscar  

    y solicitar un asiento, el usuario solicitante puede comunicarse a través de un chat con  

    el usuario oferente, llegando a un acuerdo de precio y reservando el asiento si el 

    intercambio fue exitoso.  

     

    Con esta idea en mente, mi trabajo base provee las funciones 

    bases que va a tener luego el proyecto completo: la carga de viajes con la información 

    pertinente, la solicitud de asientos y la posible eliminación de los viajes (las cuales a  

    futuro no tendrán como condición el id del chofer, sino que se realizara un chequeo de 

    seguridad del usuario). 
