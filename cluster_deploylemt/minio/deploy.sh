sudo kubectl apply -f minio-storage.yaml \
&& sleep 10 \
&&  sudo kubectl  apply -f minio.yaml \
&& sleep 10 \
&&  sudo kubectl  apply -f minio-service.yaml 
