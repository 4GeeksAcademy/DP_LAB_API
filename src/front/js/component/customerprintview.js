import React from 'react';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

const MyComponent = () => {
    const printRef = React.useRef();

    const handlePrint = () => {
        const input = printRef.current;
        html2canvas(input, { scale: 2 }).then((canvas) => {
            const imgData = canvas.toDataURL('image/png');
            const pdf = new jsPDF();
            const imgWidth = 190;
            const pageHeight = pdf.internal.pageSize.height;
            const imgHeight = (canvas.height * imgWidth) / canvas.width;

            let heightLeft = imgHeight;

            let position = 0;

            pdf.addImage(imgData, 'PNG', 10, position, imgWidth, imgHeight);
            heightLeft -= pageHeight;

            while (heightLeft >= 0) {
                position = heightLeft - imgHeight;
                pdf.addPage();
                pdf.addImage(imgData, 'PNG', 10, position, imgWidth, imgHeight);
                heightLeft -= pageHeight;
            }

            pdf.save('download.pdf');
        });
    };

    const handlePrintView = () => {
        window.print();
    };

    return (
        <div>
            <div ref={printRef} style={{ padding: '20px', border: '1px solid black' }}>
                <h1>Mi Diseño</h1>
                <p>Este es el contenido que quiero imprimir y descargar como PDF.</p>
                {/* Agrega más contenido aquí */}
            </div>
            <button onClick={handlePrint}>Descargar como PDF</button>
            <button onClick={handlePrintView}>Imprimir Vista</button>
        </div>
    );
};

export default MyComponent;