import asyncio
import json
import websockets
import requests
import signal
import sys
import logging
import argparse

import random
import string
def ran_subdomain(longueur=8):
    lettres = string.ascii_lowercase
    return ''.join(random.choice(lettres) for _ in range(longueur))


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DEFAULT_SUBDOMAIN = ran_subdomain()
DEFAULT_SERVER = "ws://18.222.145.185:8765"
DEFAULT_PORT = 3000

SUBDOMAIN = None
SERVER = None  
LOCAL_TARGET = None

shutdown_event = asyncio.Event()




def signal_handler(signum, frame):
    logger.info(f"Signal {signum} reçu (Ctrl+C), arrêt en cours...")
    shutdown_event.set()

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Client tunnel - Expose votre service local via un tunnel sécurisé',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python client.py
  python client.py -t mon-tunnel -p 8080
  python client.py --tunnel api --port 5000
  python client.py -t webapp -p 3000 -s ws://autre-serveur:8765
        """
    )
    
    parser.add_argument(
        '-t', '--tunnel', 
        default=DEFAULT_SUBDOMAIN,
        help=f'Nom du tunnel/sous-domaine (défaut: {DEFAULT_SUBDOMAIN})'
    )
    
    parser.add_argument(
        '-p', '--port', 
        type=int, 
        default=DEFAULT_PORT,
        help=f'Port du service local (défaut: {DEFAULT_PORT})'
    )
    
    # parser.add_argument(
    #     '-s', '--server', 
    #     default=DEFAULT_SERVER,
    #     help=f'Adresse du serveur WebSocket (défaut: {DEFAULT_SERVER})'
    # )
    
    parser.add_argument(
        '--host', 
        default='localhost',
        help='Host du service local (défaut: localhost)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Mode verbose (plus de logs)'
    )
    
    return parser.parse_args()

async def handle_http_request(data, websocket):
    try:
        if args.verbose:
            logger.info(f"Requête {data['method']} {data['url']}")
        resp = requests.request(
            method=data["method"],
            url=LOCAL_TARGET + data["url"],
            headers=data.get("headers", {}),
            data=data.get("body", None),
            timeout=10
        )
        response_payload = {
            "type": "httpResponse",
            "request_id": data.get("request_id"),
            "status": resp.status_code,
            "headers": dict(resp.headers),
            "body": resp.text,
        }
        if args.verbose:
            logger.info(f"Réponse: {resp.status_code}")
        
    except requests.exceptions.ConnectionError:
        logger.error(f"Impossible de se connecter à {LOCAL_TARGET}")
        logger.error("Vérifiez que TN service local est démarré")
        response_payload = {
            "type": "httpResponse",
            "request_id": data.get("request_id"),
            "status": 502,
            "headers": {},
            "body": f"Service local indisponible sur {LOCAL_TARGET}",
        }
    except requests.exceptions.Timeout:
        logger.error("Timeout sur la requete locale blablabla" )
        response_payload = {
            "type": "httpResponse",
            "request_id": data.get("request_id"),
            "status": 504,
            "headers": {},
            "body": "Timeout sur le service local",
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur requête locale: {e}")
        response_payload = {
            "type": "httpResponse",
            "request_id": data.get("request_id"),
            "status": 500,
            "headers": {},
            "body": f"Erreur client: {str(e)}",
        }

    await websocket.send(json.dumps(response_payload))

async def main():
    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)
    
    websocket = None
    reconnect_attempts = 0
    max_reconnect_attempts = 5
    
    while not shutdown_event.is_set() and reconnect_attempts < max_reconnect_attempts:
        try:
            logger.info(f"connectioon .....{SERVER}...")
            websocket = await websockets.connect(SERVER)
            reconnect_attempts = 0
            register_msg = {"type": "register", "subdomain": SUBDOMAIN}
            await websocket.send(json.dumps(register_msg))
            logger.info(f"demande de reation du domaine  {SUBDOMAIN}.aiko.qzz.io")
            while not shutdown_event.is_set():
                try:
                    msg = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(msg)
                    if data.get("type") == "http":
                        await handle_http_request(data, websocket)
                    elif data.get("type") == "ok":
                        logger.info(f"Tunnel {SUBDOMAIN}.aiko.qzz.io activé avec succès!")
                        logger.info(f"  {LOCAL_TARGET} ---->")
                        logger.info(f"    https://{SUBDOMAIN}.aiko.qzz.io")
                except asyncio.TimeoutError:
                    continue
                except websockets.exceptions.ConnectionClosed:
                    logger.warning("Connexion fermée par le serveur")
                    break
                except json.JSONDecodeError as e:
                    logger.error(f"Erreur décodage JSON: {e}")
                    continue
        except websockets.exceptions.ConnectionRefused:
            reconnect_attempts += 1
            logger.error(f"Connexion refusée (tentative {reconnect_attempts}/{max_reconnect_attempts})")
            if reconnect_attempts < max_reconnect_attempts:
                logger.info("Nouvelle tentative dans 5 secondes...")
                await asyncio.sleep(5)
            else:
                logger.error("Nombre maximum de tentatives de connexion atteint")
                break
        except websockets.exceptions.InvalidURI:
            logger.error(f"URL WebSocket invalide: {SERVER}")
            break
        except Exception as e:
            reconnect_attempts += 1
            logger.error(f"Erreur de connexion: {e} (tentative {reconnect_attempts}/{max_reconnect_attempts})")
            if reconnect_attempts < max_reconnect_attempts:
                logger.info("reconnexion dan 5 secondes...")
                await asyncio.sleep(5)
            else:
                logger.error("Nombre maximum de tentatives de connexion atteint")
                break
        finally:
            if websocket:
                logger.info("deconnexion WebSocket...")
                await websocket.close()
    logger.info("Client tunnel stop")

if __name__ == "__main__":
    args = parse_arguments()
    SUBDOMAIN = args.tunnel
    SERVER = DEFAULT_SERVER
    LOCAL_TARGET = f"http://{args.host}:{args.port}"
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    print("tunfox ...")
    print("=" * 60)
    print(f"📡 Serveur WebSocket: {SERVER}")
    print(f"🌐 Tunnel public:     https://{SUBDOMAIN}.aiko.qzz.io")
    print(f"🏠 Service local:     {LOCAL_TARGET}")
    print(f"📊 Mode verbose:      {'Activé' if args.verbose else 'Désactivé'}")
    print("=" * 60)
    print("💡 Appuyez sur Ctrl+C pour arrêter le tunnel")
    print()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 stoping tunnel ...")
    except Exception as e:
        print(f"\n💥 Erreur fatale: {e}")
        sys.exit(1)
    finally:
        print("👋 Client tunnel arrêté - Au revoir!")
