GCP Setup

- Create a VM instance
- Install [Docker on VM](https://docs.dwani.ai/discovery/docker_setup.html)
    - 

Open Issue :
- Access UX from GCP machine : port binding ? <18789> <80>
- Whatsapp - QR Link Not working


- Command for VM creation 

 CLI


 gcloud compute instances create open-claw-whatspp --project=my-google-project-id --zone=us-central1-b --machine-type=e2-micro --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default --maintenance-policy=MIGRATE --provisioning-model=STANDARD --service-account=my-servicee-account-email@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/trace.append --tags=http-server,https-server --create-disk=auto-delete=yes,boot=yes,device-name=open-claw-whatspp,image=projects/ubuntu-os-cloud/global/images/ubuntu-minimal-2510-questing-amd64-v20260313,mode=rw,size=50,type=pd-balanced --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --labels=goog-ec-src=vm_add-gcloud --reservation-affinity=any

 --

-- 
rest API

 POST https://compute.googleapis.com/compute/v1/projects/my-google-project-id/zones/us-central1-b/instances
{
  "canIpForward": false,
  "confidentialInstanceConfig": {
    "enableConfidentialCompute": false
  },
  "deletionProtection": false,
  "description": "",
  "disks": [
    {
      "autoDelete": true,
      "boot": true,
      "deviceName": "open-claw-whatspp",
      "diskEncryptionKey": {},
      "initializeParams": {
        "diskSizeGb": "50",
        "diskType": "projects/my-google-project-id/zones/us-central1-f/diskTypes/pd-balanced",
        "labels": {},
        "sourceImage": "projects/ubuntu-os-cloud/global/images/ubuntu-minimal-2510-questing-amd64-v20260313"
      },
      "mode": "READ_WRITE",
      "type": "PERSISTENT"
    }
  ],
  "displayDevice": {
    "enableDisplay": false
  },
  "guestAccelerators": [],
  "instanceEncryptionKey": {},
  "keyRevocationActionType": "NONE",
  "labels": {
    "goog-ec-src": "vm_add-rest"
  },
  "machineType": "projects/my-google-project-id/zones/us-central1-b/machineTypes/e2-micro",
  "metadata": {
    "items": []
  },
  "name": "open-claw-whatspp",
  "networkInterfaces": [
    {
      "accessConfigs": [
        {
          "name": "External NAT",
          "networkTier": "PREMIUM"
        }
      ],
      "stackType": "IPV4_ONLY",
      "subnetwork": "projects/my-google-project-id/regions/us-central1/subnetworks/default"
    }
  ],
  "params": {
    "resourceManagerTags": {}
  },
  "reservationAffinity": {
    "consumeReservationType": "ANY_RESERVATION"
  },
  "scheduling": {
    "automaticRestart": true,
    "onHostMaintenance": "MIGRATE",
    "provisioningModel": "STANDARD"
  },
  "serviceAccounts": [
    {
      "email": "my-servicee-account-email@developer.gserviceaccount.com",
      "scopes": [
        "https://www.googleapis.com/auth/devstorage.read_only",
        "https://www.googleapis.com/auth/logging.write",
        "https://www.googleapis.com/auth/monitoring.write",
        "https://www.googleapis.com/auth/service.management.readonly",
        "https://www.googleapis.com/auth/servicecontrol",
        "https://www.googleapis.com/auth/trace.append"
      ]
    }
  ],
  "shieldedInstanceConfig": {
    "enableIntegrityMonitoring": true,
    "enableSecureBoot": false,
    "enableVtpm": true
  },
  "tags": {
    "items": [
      "http-server",
      "https-server"
    ]
  },
  "zone": "projects/my-google-project-id/zones/us-central1-b"
}

-- 
TerraForm 

# This code is compatible with Terraform 4.25.0 and versions that are backwards compatible to 4.25.0.
# For information about validating this Terraform code, see https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/google-cloud-platform-build#format-and-validate-the-configuration

resource "google_compute_instance" "open-claw-whatspp" {
  boot_disk {
    auto_delete = true
    device_name = "open-claw-whatspp"

    initialize_params {
      image = "projects/ubuntu-os-cloud/global/images/ubuntu-minimal-2510-questing-amd64-v20260313"
      size  = 50
      type  = "pd-balanced"
    }

    mode = "READ_WRITE"
  }

  can_ip_forward      = false
  deletion_protection = false
  enable_display      = false

  labels = {
    goog-ec-src = "vm_add-tf"
  }

  machine_type = "e2-micro"
  name         = "open-claw-whatspp"

  network_interface {
    access_config {
      network_tier = "PREMIUM"
    }

    queue_count = 0
    stack_type  = "IPV4_ONLY"
    subnetwork  = "projects/my-google-project-id/regions/us-central1/subnetworks/default"
  }

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    preemptible         = false
    provisioning_model  = "STANDARD"
  }

  service_account {
    email  = "my-servicee-account-email@developer.gserviceaccount.com"
    scopes = ["https://www.googleapis.com/auth/devstorage.read_only", "https://www.googleapis.com/auth/logging.write", "https://www.googleapis.com/auth/monitoring.write", "https://www.googleapis.com/auth/service.management.readonly", "https://www.googleapis.com/auth/servicecontrol", "https://www.googleapis.com/auth/trace.append"]
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }

  tags = ["http-server", "https-server"]
  zone = "us-central1-b"
}
