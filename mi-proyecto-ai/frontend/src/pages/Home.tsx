import { FileUploader } from '../components/FileUploader';

export function Home() {
  return (
    <div className="home">
      <h1>Procesador de IA</h1>
      <p>Sube tus archivos y procesalos con diferentes modelos de IA</p>
      <FileUploader />
    </div>
  );
}
